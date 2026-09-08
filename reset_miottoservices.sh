
#sudo docker compose -f /home/adminroot/services/run/MiottoServices_dc.prod.yml down
sudo docker compose -f /home/adminroot/services/run/MiottoServices_dc.prod.yml down
#sudo docker volume rm Miotto_iam
#sudo docker volume create Miotto_iam
sudo docker compose -f /home/adminroot/services/run/MiottoServices_dc.prod.yml build --no-cache
#sudo docker compose -f /home/adminroot/services/run/MiottoServices_dc.dev.yml build --no-cache
sudo docker compose -f /home/adminroot/services/run/MiottoServices_dc.prod.yml up -d 
#sudo docker compose -f /home/adminroot/services/run/MiottoServices_dc.dev.yml up -d
#sudo docker system prune -f