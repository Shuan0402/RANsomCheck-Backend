# RANsomCheck-Backend
## service
1. conda activate backend
2. cd /home/ubuntu/project/RANsomCheck-Backend
flask run
## background program
1. tmux at -t backend
   flask run
2. tmux at -t cuckoo
   cuckoo -d
3. tmux at -t cuckooProcess
   cuckoo process p1d
4. tmux at -t cuckooAPI
   cuckoo api -H 140.124.181.155 --port 1337 
