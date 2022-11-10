from datetime import datetime

from aiohttp import web
from gino import Gino

PG_DSN = f"postgres://aiohttp:1234@127.0.0.1:5431/aiohttp"

app = web.Application()
db = Gino()


class PostModel(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, default=datetime.today)
    owner_name = db.Column(db.String, nullable=False)

    _idx = db.Index('app_posts', 'title', unique=True)


class PostsView(web.View):

    async def get(self):
        post_id = self.request.match_info['post_id']
        post = await PostModel.get(int(post_id))
        if post is None:
            raise web.HTTPNotFound()
        return web.json_response({"title": post.title, "owner": post.owner_name})

    async def post(self):
        json_data = await self.request.json()
        new_post = await PostModel.create(**json_data)

        # Позже подкрутить валидацию, пока считаем, что данные валидны. Тренировка.
        return web.json_response({"new_post": new_post.title, "owner": new_post.owner_name})

    async def delete(self):
        post_id = int(self.request.match_info['post_id'])
        post = await PostModel.get(int(post_id))
        if post is None:
            raise web.HTTPNotFound()
        await post.delete()

        return web.json_response({"status": "deleted"})


async def init_orm(app: web.Application):
    # Выполняется на момент старта приложений
    print("Приложение стартовало")
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()

    # Выполняется, когда приложение завершает свою работу
    print("Приложение завершило работу")


app.router.add_route("POST", "/post/", PostsView)
app.router.add_route("GET", "/post/{post_id:\d+}", PostsView)
app.router.add_route("DELETE", "/post/{post_id:\d+}", PostsView)

app.cleanup_ctx.append(init_orm)

web.run_app(app)
