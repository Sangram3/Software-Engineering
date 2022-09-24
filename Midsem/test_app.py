import pytest
import sender_server
import coverage

# xml = 0
# @
# def dummy_sender():

def test_app():
    # global xml
    xml =   "   <Message>                                                            \
                    <Sender>http://127.0.0.1:4444</Sender>                           \
                    <MessageType>type2</MessageType>                                 \
                    <MessageUUID>573fbfa0-97e7-11ec-8fbc-bf1589110003</MessageUUID>  \
                    <Body>                                                           \
                        <![CDATA[                                                    \
                        GOOG,INFY,AAPL                                               \
                        ]]>                                                          \
                    </Body>                                                          \
                </Message>                                                           \
            "
    sender_server.xml = xml
    sender_server.main()
    status_code =sender_server.sender_home()
    print(status_code,'\n-------------\n\n\n')
    assert status_code=='200'

if __name__ == "__main__":
    test_app()