import os
import paramiko

def backup_to_sftp(local_path, sftp_server, sftp_username, sftp_password):
    try:
        transport = paramiko.Transport((sftp_server, 22))
        transport.connect(username=sftp_username, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        def upload_dir(local_dir, remote_dir):
            for item in os.listdir(local_dir):
                local_item = os.path.join(local_dir, item)
                remote_item = os.path.join(remote_dir, item)
                if os.path.isdir(local_item):
                    try:
                        sftp.mkdir(remote_item)
                    except:
                        pass
                    upload_dir(local_item, remote_item)
                else:
                    sftp.put(local_item, remote_item)

        upload_dir(local_path, "/backup")
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Error during SFTP backup: {e}")
