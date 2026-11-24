import pytest
from src.manager import Manager
from src.models import Parameters, Transfer


def test_settlement_data_integrity():
    params = Parameters(
        apartments_json_path="data/apartments.json",
        tenants_json_path="data/tenants.json",
        transfers_json_path="data/transfers.json",
        bills_json_path="data/bills.json",
    )
    manager = Manager(params)

    apartment_key = "apart-polanka"
    year = 2024
    month = 1

    total_apartment_costs = manager.get_apartment_costs(apartment_key, year, month)
    assert total_apartment_costs is not None

    apartment_settlement = manager.get_settlement(apartment_key, year, month)
    assert apartment_settlement is not None
    assert apartment_settlement.total_due_pln == pytest.approx(total_apartment_costs)

    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)
    assert tenants_settlements is not None
    assert len(tenants_settlements) > 0

    total_tenants_due = sum(ts.total_due_pln for ts in tenants_settlements)
    assert total_tenants_due == pytest.approx(total_apartment_costs)
    assert total_tenants_due == pytest.approx(apartment_settlement.total_due_pln)

def test_get_tax():
    params = Parameters()
    manager = Manager(params)

    manager.transfers = [
        Transfer(amount_pln=2500.0, date="2025-01-04", settlement_year=2025, settlement_month=1, tenant="tenant-1"),
        Transfer(amount_pln=2500.0, date="2025-01-05", settlement_year=2025, settlement_month=1, tenant="tenant-2"),
        Transfer(amount_pln=2500.0, date="2025-01-06", settlement_year=2025, settlement_month=1, tenant="tenant-3"),
        Transfer(amount_pln=1000.0, date="2025-02-05", settlement_year=2025, settlement_month=2, tenant="tenant-1"),
    ]

    assert manager.get_tax(2025, 1, 0.085) == 638
    assert manager.get_tax(2025, 2, 0.085) == 85
    assert manager.get_tax(2025, 3, 0.085) == 0