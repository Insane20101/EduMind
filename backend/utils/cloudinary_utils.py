import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary using the CLOUDINARY_URL env variable automatically
# (cloudinary library reads CLOUDINARY_URL from environment by default)
cloudinary.config(
    cloudinary_url=os.getenv("CLOUDINARY_URL")
)

def upload_pdf(file_bytes: bytes, filename: str, folder: str) -> dict:
    """
    Uploads a PDF file to Cloudinary under the given folder.
    Returns a dict with 'secure_url', 'public_id', 'resource_type'.
    """
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,
        public_id=filename.rsplit(".", 1)[0],  # strip extension
        resource_type="raw",  # 'raw' for non-image/video files like PDF
        use_filename=True,
        unique_filename=False,
        overwrite=True,
        format="pdf",
    )
    return {
        "secure_url": result["secure_url"],
        "public_id": result["public_id"],
        "resource_type": result["resource_type"],
    }

def delete_resource(public_id: str) -> dict:
    """Deletes a file from Cloudinary by its public_id."""
    return cloudinary.uploader.destroy(public_id, resource_type="raw")
