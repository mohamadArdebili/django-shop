from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from apps.product.models import Product, Category, Size, Color


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"


class NavBarPartialView(TemplateView):
    template_name = "includes/navbar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class CategoryStyle(TemplateView):
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductListView(ListView):
    template_name = "product/products_list.html"
    model = Product
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()  # Product.objects.all() by default
        req = self.request

        colors = req.GET.getlist("color")
        sizes = req.GET.getlist("size")
        min_price = req.GET.get("min_price")
        max_price = req.GET.get("max_price")

        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()
        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()
        if min_price and max_price:
            queryset = Product.objects.filter(price__lte=max_price, price__gte=min_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_sizes'] = Size.objects.all().distinct()
        context['all_colors'] = Color.objects.all().distinct()
        params = self.request.GET.copy()
        params.pop('page', None)
        context['params'] = params.urlencode()
        return context


# class ProductListView(ListView):
#     template_name = "product/products_list.html"
#
#
#     queryset = Product.objects.all()
#     paginate_by = 1
#
#
#     def get_context_data(self, **kwargs):
#         request = self.request
#
#         colors = request.GET.getlist("color")
#         sizes = request.GET.getlist("size")
#         min_price = request.GET.get("min_price")
#         max_price = request.GET.get("max_price")
#         queryset = Product.objects.all()
#         if colors:
#             queryset = Product.objects.filter(color__title__in=colors).distinct()
#         if sizes:
#             queryset = Product.objects.filter(size__title__in=sizes).distinct()
#         if min_price and max_price:
#             queryset = Product.objects.filter(price__lte=max_price, price__gte=min_price)
#         context = super(ProductListView, self).get_context_data()
#         context["object_list"] = queryset
#         return context
