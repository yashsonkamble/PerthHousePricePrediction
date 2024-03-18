There are two folders:

Phase3_FE for frontend code
Phase3_BE for backend code

In order to run the project we need to run both(frontend and backed) the codes.

To run the Backend code, we need to run the backend.py in the Phase3_BE folder with the command "python3 backend.py" and it gets hosted on localhost on port number 8000

To run the Frontend code, there are two ways that it can be done

Method 1) Go in dist folder (contains the build code of frontend code) of Phase3_FE, we just need to host the dist folder on a web server, for eg live-server plugin in vscode can be used which hosts the frontend code on port 5500

Method 2) For this method nodejs is required. Go in Phase3_FE folder, run "npm install", and then run "npm run dev". After running the previous commands the frontend code will be running on localhost port 5173
