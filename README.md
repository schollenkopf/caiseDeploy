### BUILD AND RUN THE PROJECT

- Install docker [Here if you do not have it](https://docker.com/products/docker-desktop/)

- Clone repo

- Inside repo run command 
    - First time

        docker-compose up --build

    - Otherwise

        docker-compose up
    
- After exit (^C)
    - docker-compose down 


### REMARKS OR BUGS

- Sometimes in order to apply the filter you need to press twice on the filter button

- Changing selected node is only possible in the **History Graph** view

- To download a snapshot right-click on any node in the **History Graph** view a new menu will appear in the upper-left corner

### EXAMPLE FILTER INPUTS

- Filter Out
    - A
    - A;B

- Flow Slection
    - A;B

- Throughput 
    - A;B;3600;longer
    - A;B;3600;shorter

- Remove Behavior
    - 0.8

