import socket
from packet_handler import DNSPacket
from cache import Cache

port = 53
local_ip = '127.0.0.1'
remote_ip = '8.8.8.8'


def main():
    cache = Cache()
    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.bind((local_ip, port))
            server.recvfrom(1024)
            server.recvfrom(1024)
            data, address = server.recvfrom(1024)
            request_processing = DNSPacket(data)
            info_from_cache = cache.get_record((request_processing.domain, request_processing.question_type))
            if info_from_cache:
                print("FROM CACHE")
                response = request_processing.get_response(info_from_cache)
                server.sendto(response, address)
            else:
                print("FROM DNS SERVER")
                dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                dns_socket.sendto(data, (remote_ip, port))
                dns_data, rem_address = dns_socket.recvfrom(1024)
                server.sendto(dns_data, address)
                request_processing = DNSPacket(dns_data)
                cache.add_record(request_processing.domain, request_processing.question_type, request_processing.info)
        except KeyboardInterrupt:
            break
        finally:
            cache.save()


if __name__ == '__main__':
    main()
