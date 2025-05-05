curl https://rclone.org/install.sh | sudo bash
sudo sed -i '/^#user_allow_other/s/^#//' /etc/fuse.conf
mkdir -p ~/.config/rclone
cp ./rg_rclone.conf ~/.config/rclone/rclone.conf
export RCLONE_CONTAINER=object-persist-project-22
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli