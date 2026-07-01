sudo docker compose -f /home/adminroot/services/run/Authenticate_dc.dev.yml -p authenticate down
sudo docker system prune -f
sudo docker compose -f /home/adminroot/services/run/Authenticate_dc.dev.yml -p authenticate up --build