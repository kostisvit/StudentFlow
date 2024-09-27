# forms.py
from django import forms
from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Το αρχείο υπερβαίνει το όριο των 10MB.')

class EmailForm(forms.Form):
    email = forms.EmailField(label='Προς')
    cc = forms.CharField(label='Κοινοποίηση', widget=forms.TextInput(attrs={'placeholder': 'Οι διευθύνσεις χωρίζονται με κόμμα'}),required=False)
    bcc = forms.CharField(label='Ιδιαίτ. Κοινοποίηση', widget=forms.TextInput(attrs={'placeholder': 'Οι διευθύνσεις χωρίζονται με κόμμα'}),required=False)
    subject = forms.CharField(label='Θέμα',max_length=100)
    attachments = forms.FileField(validators=[file_size],label="Επιλέξτε αρχείο",widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}), required=False)
    message = forms.CharField(label='Μήνυμα',widget = forms.Textarea)
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Field('email', css_class='form-control'),
    #         Field('subject', css_class='form-control'),
    #         Field('cc', css_class='form-control'),
    #         Field('bcc', css_class='form-control'),
    #         Field('attachments', css_class='form-control'),
    #         Field('message', css_class='form-control'),
    #         Submit('submit', 'Send Email', css_class='btn btn-primary')
    #     )