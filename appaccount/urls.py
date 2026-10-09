from django.urls import path
from . import views




urlpatterns = [
    
    path(  '',  views.home,  name='home' ),

    path('product/<int:product_id>/',views.product_detail,name='product_detail' ),

    path( 'cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path( 'cart/', views.cart, name='cart'),


    path('cart/remove/<int:product_id>/',views.remove_from_cart,name='remove_from_cart' ),

    path('cart/decrease/<int:product_id>/',views.decrease_cart,name='decrease_cart'),

    path( 'cart/increase/<int:product_id>/', views.increase_cart, name='increase_cart'),


    path("register/", views.register, name="register"),

    path("login/", views.login_view, name="login"),


    path("logout/", views.logout_view, name="logout"),


   path('categories/', views.categories_view, name='categories'),

    # Single category products
    path('category/<int:category_id>/',views.category_products,name='category_products' ),
 
 
 
  path('buy-now/<str:item_type>/<int:item_id>/',views.buy_now,name='buy_now'),
  
    # Buy Now
    



    # Checkout
    path('checkout/',views.checkout,name='checkout'),




    # =====================================================
    # SUBCATEGORY
    # =====================================================



   path( 'search/',views.search_products,name='search_products'),

   path('search-suggestions/',views.search_suggestions,name='search_suggestions'),

# Shoes
  path( "shoes/", views.shoes, name="shoes"),

 
  path('makeup/', views.makeup, name='makeup'),
  
    # Electronics page
  path( 'electronics/', views.electronics, name='electronics'),

  path( 'watches/', views.watches, name='watches' ),
  
  
  path( 'accessories/', views.accessories, name='accessories' ),
  
  
  
  path('about/', views.about, name='about'),
  
  path('contact/', views.contact, name='contact'),

   





# Shoes page
]





  



  








   





