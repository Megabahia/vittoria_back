import boto3
import environ


class AwsS3:
    def __init__(self):
        # environ init
        self.env = environ.Env()
        environ.Env.read_env()  # LEE ARCHIVO .ENV
        self.s3 = self.configurar_s3_cliente(self.env)

    def configurar_s3_cliente(self, env):
        return boto3.client(
            's3',
            aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY')
        )

    def get_file_url(self, file_type, key):
        """
        Obtiene un archivo desde S3.

        Parameters:
        - clave (str): La clave del archivo.

        Returns:
        - object: Objeto del archivo si existe, 'No existe' en caso contrario.
        """
        file_path = f"PRODUCTOS_EXTERNOS/{file_type}/{key}"
        try:
            self.s3.get_object(Bucket=self.env.str('AWS_STORAGE_BUCKET_NAME'), Key=file_path + ".png")
            return f"https://{self.env.str('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/{file_path}.png"
        except self.s3.exceptions.NoSuchKey:
            try:
                self.s3.get_object(Bucket=self.env.str('AWS_STORAGE_BUCKET_NAME'), Key=file_path + ".jpeg")
                return f"https://{self.env.str('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/{file_path}.jpeg"
            except self.s3.exceptions.NoSuchKey:
                try:
                    self.s3.get_object(Bucket=self.env.str('AWS_STORAGE_BUCKET_NAME'), Key=file_path + ".jpg")
                    return f"https://{self.env.str('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com/{file_path}.jpg"
                except self.s3.exceptions.NoSuchKey:
                    return None

    def get_foto_frente_url(self, key):
        """
        Retrieves the URL of the "FOTO_FRENTE" file for the given key.

        Args:
            key (str): The unique identifier of the file.

        Returns:
            str: The URL of the file if found, None otherwise.
        """
        return self.get_file_url("FOTO_FRENTE", key)

    def get_foto_bonita_url(self, key):
        """
        Retrieves the URL of the "FOTO_BONITA" file for the given key.

        Args:
            key (str): The unique identifier of the file.

        Returns:
            str: The URL of the file if found, None otherwise.
        """
        return self.get_file_url("FOTO_BONITA", key)

    def get_foto_original_url(self, key):
        """
        Retrieves the URL of the "FOTO_ORIGINAL" file for the given key.

        Args:
            key (str): The unique identifier of the file.

        Returns:
            str: The URL of the file if found, None otherwise.
        """
        return self.get_file_url("FOTO_ORIGINAL", key)
