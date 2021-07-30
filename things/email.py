from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activation.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['var'] = "Hello world"
        return context