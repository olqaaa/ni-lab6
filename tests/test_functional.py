import pytest
from src.manager import Manager
from src.models import Parameters


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