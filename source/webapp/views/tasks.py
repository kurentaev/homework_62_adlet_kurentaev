from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Tasks
from webapp.forms import TasksListForm


class SuccessDetailUrlMixin:
    def get_success_url(self):
        return reverse('todo_detail', kwargs={'pk': self.object.pk})


class TaskAddView(PermissionRequiredMixin, SuccessDetailUrlMixin, LoginRequiredMixin, CreateView):
    template_name = 'task/task_create.html'
    form_class = TasksListForm
    model = Tasks
    permission_required = 'webapp.create_task'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user


class TaskUpdateView(PermissionRequiredMixin, SuccessDetailUrlMixin, LoginRequiredMixin, UpdateView):
    template_name = 'task/task_update.html'
    form_class = TasksListForm
    model = Tasks
    context_object_name = 'task'
    permission_required = 'webapp.change_task'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user


class TaskView(DetailView):
    template_name = 'task/task.html'
    model = Tasks
    context_object_name = 'task'


class TaskDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'task/task_delete.html'
    model = Tasks
    context_object_name = 'task'
    success_url = reverse_lazy('index')
    permission_required = 'webapp.delete_task'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user
