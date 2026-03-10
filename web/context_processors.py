def seller_status(request):
    if request.user.is_authenticated:
        has_pending_seller = request.user.seller_set.filter(status='pending').exists()
    else:
        has_pending_seller = False
    return {
        'has_pending_seller': has_pending_seller
    }
