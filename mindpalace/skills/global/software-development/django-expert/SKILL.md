---
name: django-expert
description: "Use when building Django 5.0 web apps or REST APIs with Django REST Framework. Invoke for models.py, settings.py, manage.py; building DRF serializers/viewsets, optimizing ORM queries (select_related/prefetch_related), JWT auth. Triggers: Django, DRF, Django REST Framework, Django ORM, Django model, serializer, viewset, Python web."
version: 1.0.0
license: MIT
tags: [django, drf, python, orm, rest-api, jwt, serializers, viewsets]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/django-expert
derived_from: awesomeclaude
---

# Django Expert

Django 5.0 + Django REST Framework, production-grade.

## When to use

Django web apps / REST APIs; model design with relationships; DRF serializers + viewsets; ORM query optimization; JWT/session auth; admin customization.

## Core workflow

1. **Analyze** — models, relationships, API endpoints.
2. **Design models** — fields, indexes, managers → `makemigrations` + `migrate`; verify schema.
3. **Implement views** — DRF viewsets or Django async views.
4. **Validate endpoints** — quick `APITestCase`/`curl` for status codes before adding auth.
5. **Add auth** — permissions, SimpleJWT.
6. **Test** — `TestCase`, `APITestCase`.

## Key pattern

```python
class Article(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="articles")
    published_at = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        indexes = [models.Index(fields=["author", "published_at"])]

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return Article.objects.select_related("author").all()  # avoids N+1
```

## Constraints

MUST: `select_related`/`prefetch_related` for relations; DB indexes on hot query fields; env vars for secrets; permissions on every endpoint; tests for models + endpoints; built-in security (CSRF, etc.).
MUST NOT: raw SQL without parameterization; skip migrations; secrets in settings.py; `DEBUG=True` in prod; trust input without validation; ignore query optimization.

## Output

1. Models with indexes. 2. Serializers with validation. 3. ViewSets/views with permissions. 4. Brief note on query optimization.

## Knowledge

Django 5.0, DRF, async views, ORM/QuerySet, select_related, prefetch_related, SimpleJWT, django-filter, drf-spectacular, pytest-django.
