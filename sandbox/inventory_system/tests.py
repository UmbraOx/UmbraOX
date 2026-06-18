# Tests for the inventory system
def test_list_products():
    assert list_products() == []

def test_add_product():
    add_product('Test Product', 10)
    assert len(list_products()) == 1