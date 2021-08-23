import asyncio
from datetime import datetime
from pubsub import PubSub

c = {
    "type":
    "service_account",
    "project_id":
    "jorjoran",
    "private_key_id":
    "718817ff5079b918df5c206fb87b275c8a212ff4",
    "private_key":
    "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnjPlae+SGp5pw\nqDz7CJsLIGZHPYJoC+5rR4cNgUV8KDtzgMLxPEa51Bk+p0mYwEC2pWFlHL+pc+Kx\nHvcNZOQOYBHKl3ijKycAufh6TcB02uzm2vOUKFWfZGTS2WOyCc5eJhcnDFM+u8KH\nNh6erWVS2fN/EaBkIOx8k2m26rxq2ZJ4/XAwkP+yxh+t9vMg9QUnVlIX9eYIHD6X\n8H19a5W8MFdzvxnS9iey9j0SkVOzCx2CTyMJ+MvwpC+/SQk6cUS/JcmPWl0RXWV9\nPbc+pVvzfIELqxcfZwaODsiq5+XlY96o6FKrbl1LNVNrhJr/2LLlDOz+wny/cfhk\ntYuLWQFHAgMBAAECggEAAMi3Od7QrU3skv3uzv2IQRtM9vdpEvjsnHdTD0UFn90D\njxwAl9plnQoZJIfyIWnb3Xi+Y6QgUJLYBtIHJTiLnCPvAu2Wl7yeUBK4AJesfIa6\nH9h+xY9kb7I39WcU5FEydmC2BvXQvYWKcG5xFD1VGCVaDB77eov0ge0+zAJcvkHU\n5fRXK5KiyQYH97FHadtgbTbfJLS0LAKdZV+7a0XfIKHKeS8wsWJ4G6KC6FcxUU+3\nThMZQiMq63uVvKxP5i/l29NHJwUxNBEhDcEWd2lk08RFCBIti4T2oLiuDXZ+58zY\n+CiGFj4/pshMZURJFrVkIUZpvU3XovNbOaznVHdhkQKBgQDS/XB7b4gFPt+OE4Gi\nCG573eWfO+9m5FJmIt2hVXFbgQIkW8VcaQFS9StoiFbwTtllUzNOZXg6bn6XnlCQ\nbkjuhLDYRQP4+q1OGgJsk/VPt0pWCXjDycAPYwkXzr1LJmnxDHlcSZkJRiolnEVb\n/yVNzKQ5DkryMqen+MX3/F9GGQKBgQDLSztXpoMC3n+a9mYDpYE11G75D+hb6jve\nHxhInbRP/8QEZSJsEhdYRr2IdWkEDRUemkQ2mKzskqm0rAmGJAepla5RF4ijt63j\n6zSJgKmnsDoCw4XhCZ2Gk/G827VuePSZszTWLtJfkpbyH8jDtOBPZrEZULR5U98X\nChu0xkGuXwKBgFH940RUp0tCj6Wqtum81RKVvLIQnIwjllHSosYbah3hGHAAqcWr\nmLQgSmoo8YAZZCoYFwwUKpCqd8972lsGQJlQP1kMGOscn1SGjwKazO3ZkK22qJON\nR3GzTslNsgoON4VRD6hpgWs1NRPAksOZd2mwaPEzOLS+MqD38BbaoDuhAoGARTFL\n919DRBy6zeGDg0Y3njy5sKfLbE1jJwzqVPzoPDpPWzeY6bOWooMhS2q63ZgeUhYr\nlXGNmc+pV0cezrtAqGW7uPoLlb2Uv/h0H0DdfaerdvlZfeip5v4/zwnwzLL6fb3T\nA/tXuxPHsI1E5eeQWTYYnQctBgaX7d2Q5Ix+Gn0CgYEAj0W9jmRyppxEBORzkXUU\na8OjJBjO1BL28pDJ//g+p/URtJGuu8z7QCprGBrKNb/JSYI+lXrGLugJ5JQwzEFk\ndvBjU2iUT3wE/kuvUhCaf1fTlmSTPb/0NEZWsB3rZTYivffd5NCYZzEIPSBvXY8p\nsZqbchvj3n3OsIMYyn+AV0o=\n-----END PRIVATE KEY-----\n",
    "client_email":
    "afniaaa@jorjoran.iam.gserviceaccount.com",
    "client_id":
    "110845275204492472701",
    "auth_uri":
    "https://accounts.google.com/o/oauth2/auth",
    "token_uri":
    "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":
    "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url":
    "https://www.googleapis.com/robot/v1/metadata/x509/afniaaa%40jorjoran.iam.gserviceaccount.com"
}


async def executor(data):
    print("{}".format(data.data), datetime.now())


async def sublistener(config, subname, count=1):
    '''Pubsub listen subscribtion tasks'''
    p = PubSub(c)
    while True:
        subscrb = p.sub()
        with subscrb:
            subpath = subscrb.subscription_path(config["project_id"], subname)

            # get messages
            response = subscrb.pull(request={
                'subscription': subpath,
                'max_messages': count
            })

            ack_ids = []
            for msg in response.received_messages:

                # print("Received: {}".format(msg.message))
                await executor(msg.message)

                ack_ids.append(msg.ack_id)

            # Acknowledges the received messages so they will not be sent again.
            tot = len(response.received_messages)
            if tot > 0:
                subscrb.acknowledge(request={
                    "subscription": subpath,
                    "ack_ids": ack_ids,
                })

        await asyncio.sleep(2)


# begin
async def main_pubsub(c):
    await sublistener(c, 'test001-sub', 10)


if __name__ == '__main__':

    loop = asyncio.new_event_loop()
    try:
        loop.create_task(main_pubsub(c))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
    finally:
        loop.close()
