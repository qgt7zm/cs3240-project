from django.db import models

from allauth.socialaccount.models import SocialAccount
from storages.backends.s3boto3 import S3Boto3Storage


# Helper Classes


class CustomS3Boto3Storage(S3Boto3Storage):
    # User upload directory on Amazon S3
    location = 'uploads/'


class SubmissionStatus:
    NOT_REVIEWED = 'Not Yet Reviewed'  # This file has not been seen by an admin
    IN_PROGRESS = 'In Progress'  # This file has been seen by an admin
    RESOLVED = 'Resolved'  # This file has been resolved by an admin
    UNRESOLVED = "Unresolved"

    choices = [NOT_REVIEWED, IN_PROGRESS, RESOLVED, UNRESOLVED]


class ReportCategory:
    MENTAL_HEALTH = 'General Mental Health'
    ACADEMIC = 'Academic'
    SUBSTANCE_ABUSE = 'Substance Abuse'
    OTHER = 'Other'

    choices = [MENTAL_HEALTH, ACADEMIC, SUBSTANCE_ABUSE, OTHER]


status_colors = {
    SubmissionStatus.NOT_REVIEWED: 'slategray',
    SubmissionStatus.IN_PROGRESS: '#c48f3f',
    SubmissionStatus.RESOLVED: 'green',
    SubmissionStatus.UNRESOLVED: "red",
}


# Model Classes

class SiteUser(models.Model):
    """A user of the website who has logged in."""
    oauth_user = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, null=True)  # The Google user
    username = models.CharField(max_length=200)  # The user's display name
    email = models.CharField(max_length=200)  # The user's login email
    is_admin = models.BooleanField(default=False)  # Whether the user is a site admin, off by default
    profile_image = models.CharField(max_length=300, null=True, blank=True)  # URL to the S3 stored image

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"


class UserFile(models.Model):
    """A file uploaded to the website by a user."""

    user = models.ForeignKey(
        SiteUser, on_delete=models.CASCADE, null=True
    )  # The user who uploaded the file, null if anonymous
    location = models.CharField(max_length=300)  # The AWS link
    file = models.FileField(storage=CustomS3Boto3Storage(), null=True)  # The storage backend, TODO try to make not null
    profile_picture = models.FileField(storage=CustomS3Boto3Storage(), null=True)
    # These fields were moved to ReportForm
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)  # The time of upload

    def get_username(self) -> str:
        """Get the username of the file uploader."""
        return "Anonymous" if self.user is None else self.user.username

    def get_filename(self) -> str:
        """Get the filename of the file without the path."""
        return self.location.split('/')[-1]

    def get_extension(self) -> str:
        """Get the extension of the file in lowercase."""
        return self.get_filename().split('.')[-1].lower()

    def __str__(self) -> str:
        return f"{self.get_filename()} ({self.get_username()})"


class ReportForm(models.Model):
    """A report submitted to the website by a user."""
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True)
    user_file = models.ForeignKey(UserFile, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=(
        (ReportCategory.MENTAL_HEALTH, ReportCategory.MENTAL_HEALTH),
        (ReportCategory.ACADEMIC, ReportCategory.ACADEMIC),
        (ReportCategory.SUBSTANCE_ABUSE, ReportCategory.SUBSTANCE_ABUSE),
        (ReportCategory.OTHER, ReportCategory.OTHER),
    ))
    summary = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)  # The time of upload

    status = models.CharField(max_length=50, choices=(
        (SubmissionStatus.NOT_REVIEWED, SubmissionStatus.NOT_REVIEWED),
        (SubmissionStatus.IN_PROGRESS, SubmissionStatus.IN_PROGRESS),
        (SubmissionStatus.RESOLVED, SubmissionStatus.RESOLVED),
    ), default='Not Yet Reviewed')  # The review status
    comments = models.TextField(max_length=1000, default='', blank=True)  # comments by the admin

    def get_username(self) -> str:
        """Get the username of the report submitted."""
        return "Anonymous" if self.user is None else self.user.username

    def get_filename(self) -> str:
        """Get the username of the report submitted."""
        return "None" if self.user_file is None else self.user_file.get_filename()

    def is_new(self) -> bool:
        """If this report has not been read by an admin yet."""
        return self.status == SubmissionStatus.NOT_REVIEWED

    def mark_in_progress(self):
        """Mark this report as read by an admin."""
        self.status = SubmissionStatus.IN_PROGRESS

    def mark_resolved(self):
        """Mark this report as resolved by an admin."""
        self.status = SubmissionStatus.RESOLVED

    def mark_unresolved(self):
        self.status = SubmissionStatus.UNRESOLVED

    def get_status_display(self) -> str:
        """Get the display value for the report status (override)."""
        return self.status

    def get_status_color(self) -> str:
        """Get the display color for the report status."""
        if self.status in status_colors.keys():
            return status_colors[self.status]
        else:
            return "black"

    def __str__(self) -> str:
        return f"{self.summary} ({self.get_username()})"
