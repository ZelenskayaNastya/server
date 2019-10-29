import asyncio
from collections import defaultdict


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    dict = defaultdict(list)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        split_data = data.split()
        getorput = split_data[0]

        if getorput not in ('get', 'put'):
            answer = 'error\nwrong command\n\n'
        else:
            answer = 'ok\n'
        if getorput == 'get':
            key = split_data[1]
            answer += self.get(key)
        elif getorput == 'put':
            valuess = split_data[1:]
            self.put(valuess)
            answer += '\n'

        return answer

    def get(self, key):
        answer = ''
        if key == '*':
            itemss = ClientServerProtocol.dict.items()
            for k, values in itemss:
                for v1, v2 in values:
                    answer += '{} {} {}\n'.format(k, v1, v2)
            answer += '\n'

        else:
            itemss = ClientServerProtocol.dict[key]
            r = []
            for (v1, v2) in itemss:
                val = [key, v1, v2]
                retl = ' '.join(val) + '\n'
                r.append(retl)
            answer = ''.join(r) + '\n'

        return answer

    def put(self, data):
        try:
            k, v1, v2 = data
            itemss = ClientServerProtocol.dict[k]
            if (v1, v2) not in itemss:
                itemss.append((v1, v2))
        except:
            print("Проверьте ввод данных")



if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
