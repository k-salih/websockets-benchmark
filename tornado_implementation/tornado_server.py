import tornado.ioloop
import tornado.web
import tornado.websocket

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    async def on_message(self, message):
        if isinstance(message, bytes):
            # Handle binary message
            print("Received binary message")
            # Echo the binary message back to the client
            await self.write_message(message, binary=True)
        else:
            # Handle text message
            print(f"Received text message: {message}")
            # Echo the text message back to the client
            await self.write_message(message)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True  # Allow connections from any origin

def make_app():
    return tornado.web.Application([
        (r"/ws", EchoWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8765)
    tornado.ioloop.IOLoop.current().start()
