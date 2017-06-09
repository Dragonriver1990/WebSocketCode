import tornado.ioloop
import tornado.web

import sockjs.tornado


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.participants, "Someone joined.")
        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        self.broadcast(self.participants, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)
        self.broadcast(self.participants, "Someone left.")

if __name__ == "__main__":

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')
    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/", IndexHandler)] + ChatRouter.urls
    )
    # 3. Make Tornado app listen on port 8080
    app.listen(8088)
    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()

