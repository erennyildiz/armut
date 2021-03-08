# armut

RUN:

Dockerfiles are created already. You can clone the project from git repo. If your docker is running, project run while running folllowing command on command line at porject root.

docker-compose up

REST APIs:

post apis:
    -http://localhost:8000/register/
	    {
		    "username": "test",
		    "email": "test@test.com",
			"password": "12345"
		}
	-http://localhost:8000/login/
		{
		    "username": "test",
		    "password": "12345"
		}
	-http://localhost:8000/message/
		{
		    "sender_name": "test",
		    "receiver_name": "test2",
			"message_detail": "lorem ipsum dolor sit amet"
		}
	-http://localhost:8000/block/
	    {
		    "blocker_name": "test",
		    "blocked_name": "test2"
		}

get apis:
    -http://localhost:8000/register/

	-http://localhost:8000/login/
		
	-http://localhost:8000/message/

	-http://localhost:8000/block/
	
	-http://localhost:8000/log/

		
TEST CASE:

    I tried cover many case. I might miss some cases but following cases are covered in test procedure.
	    
		register:
			-user_registration
			-unique_username_validation
		login:
			-authentication_without_password
			-authentication_with_wrong_password
			-authentication_with_valid_data
        message and block:
		    -valid_username_message
			-wrong_username_message
			-block_user_message
