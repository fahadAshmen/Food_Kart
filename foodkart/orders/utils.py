import datetime

def generate_order_number(pk):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #202306172023 + pk
    order_number = current_time + str(pk)
    return order_number
