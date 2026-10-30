from django.db import models
from django.contrib.auth.models import User
import uuid

class Pattern(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patterns', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    grid_size = models.IntegerField(default=30)
    craft_type = models.CharField(max_length=50, default='cross-stitch')
    pattern_mode = models.CharField(max_length=20, default='rectangular')  # 'rectangular' or 'circular'
    pattern_data = models.JSONField(default=list, blank=True)
    current_row = models.IntegerField(default=0, null=True, blank=True)
    current_col = models.IntegerField(default=0, null=True, blank=True)
    pattern_instructions = models.TextField(blank=True, null=True)  # Raw pattern text
    parsed_rows = models.JSONField(default=list, blank=True)  # Parsed row data with stitch counts
    stitch_count = models.IntegerField(default=0, null=True, blank=True)  # Current stitch count
    stitch_target = models.IntegerField(default=30, null=True, blank=True)  # Target stitches for current row
    row_history = models.JSONField(default=list, blank=True)  # Completed rows history
    share_token = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        username = self.user.username if self.user else 'Guest'
        return f"{self.name} - {username}"
    
    def save(self, *args, **kwargs):
        if not self.share_token:
            self.share_token = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']