
#sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.prod.yml down
sudo docker compose -f /home/adminroot/services/run/Authenticate_dc.dev.yml down
sudo docker volume rm IAM_dev_db
sudo docker volume create IAM_dev_db
sudo docker network rm IAM_dev_net
sudo docker network create IAM_dev_net
sudo docker compose -f /home/adminroot/services/run/Authenticate_dc.dev.yml build --no-cache
#sudo docker compose -f /home/adminroot/services/run/Authenticate_dc.dev.yml build --no-cache
sudo docker compose -f /home/adminroot/services/run/Authenticate_dc.dev.yml up -d 
#sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.dev.yml up -d
sudo docker system prune -f