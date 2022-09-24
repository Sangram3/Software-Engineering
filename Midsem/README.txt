Name: Sangram Rajendra Jagadale
E.No: 2019csb1091

-This is a python application based in flask framework.

Dependencies:

-pytest   : run command 'pip install pytest'
-coverage : run command 'pip install coverage'
-flask    : run command 'pip install Flask'

Instructions:
-Download and extract the repository named 'Midsem' in your device
-You will be able to see 4 files,
	--router_service.py
	--sender_server.py
	--receiver_server.py
	--config.json
	--test_app.py

To run the application
--perform below 3 actions in 3 different terminals
 - start the router server using -> 'python router_service.py' , Terminal 1
 - start the receiver server using -> 'python receiver_server.py' Terminal 2
 - start the sender server using -> 'python sender_server.py' Terminal 3
	
 - open the url visible on the terminal 3
 - this will open the home page of the sender, which will send the message to the router
 - router will forward this message to appropriate receiver, and receive the acknowledgement
 
To test and get the coverage
--perform below 2 actions in 2 different terminals
 - start the router server using -> 'python router_service.py' , Terminal 1
 - start the receiver server using -> 'python receiver_server.py' Terminal 2

- run the following command , 'coverage run test_app.py -m' in terminal 3
- now terminate the processes running on these 3 terminals, in the following order
  1)Terminal 1
  2)Terminal 2
  3)Terminal 3
-now run 'coverage report -m' to see the coverage

 