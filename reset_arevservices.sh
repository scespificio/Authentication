
#sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.prod.yml down
sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.prod.yml down
#sudo docker volume rm Arev_iam
#sudo docker volume create Arev_iam
sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.prod.yml build --no-cache
#sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.dev.yml build --no-cache
sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.prod.yml up -d 
#sudo docker compose -f /home/adminroot/services/run/ArevServices_dc.dev.yml up -d
#sudo docker system prune -f