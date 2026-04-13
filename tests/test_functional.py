import pytest

from src.manager import Manager
from src.models import Parameters, ApartmentSettlement, TenantSettlement, Transfer, Bill

def test_if_total_due_pln_istrue():
    manager = Manager(Parameters())

    apartment_key = 'apart-polanka'
    year = 2025
    month = 1

    apartment_settlement = manager.get_settlement(apartment_key, year, month)
    
    assert apartment_settlement is not None
    assert apartment_settlement.total_due_pln > 0.0

    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)
    
    assert tenants_settlements is not None
    assert len(tenants_settlements) > 0

    sum_tenants_due = sum(tenantset.total_due_pln for tenantset in tenants_settlements)
    assert sum_tenants_due == pytest.approx(apartment_settlement.total_due_pln)


def test_if_deposit_is_correct():
    manager = Manager(Parameters())
    
    manager.transfers=[]
##wplata od razu
    manager.transfers.append(Transfer( #1
        amount_pln=3000.0,
        date="2024-01-01",
        settlement_month=None,
        settlement_year=None,
        tenant='Jan Nowak'))
## na dwa razy
    manager.transfers.append(Transfer( #2.1
        amount_pln=1000.0,
        date="2024-01-01",
        settlement_month=None,
        settlement_year=None,
        tenant='Adam Kowalski'))
    
    manager.transfers.append(Transfer( #2.2
        amount_pln=1900.0,
        date="2024-01-01",
        settlement_month=None,
        settlement_year=None,
        tenant='Adam Kowalski'))
# bledna wplata
    manager.transfers.append(Transfer( #3
        amount_pln=2000.0,
        date="2024-01-01",
        settlement_month=2024,
        settlement_year=1,
        tenant='Ewa Adamska'))

    results = manager.check_deposits()

    assert results['tenant-1'] is True, "Opłacona kaucja"
    assert results['tenant-2'] is True, "Opłacona kaucja"
    assert results['tenant-3'] is False, "Błędna wpłata"

def test_if_deposits_transfers_arre_empty():
    manager = Manager(Parameters())

    manager.transfers=[]
    results = manager.check_deposits()

    for tenant_key in manager.tenants:
        assert results[tenant_key] is False