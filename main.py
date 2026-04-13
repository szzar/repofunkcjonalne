from src.manager import Manager
from src.models import Parameters
import sys

def print_section_header(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_subsection_header(title: str):
    """Print a formatted subsection header"""
    print(f"\n  {title}")
    print(f"  {'-' * 40}")


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"{amount:,.2f} PLN"


def display_apartments(manager):
    """Display all apartments with their rooms and bills"""
    print_section_header("APARTMENTS")
    
    for apartment in manager.apartments.values():
        print(f"\n📍 {apartment.name} ({apartment.key})")
        print(f"   Location: {apartment.location}")
        print(f"   Total Area: {apartment.area_m2} m²")
        
        print_subsection_header("Rooms")
        for room in apartment.rooms.values():
            print(f"      • {room.name:<25} {room.area_m2:>6} m²")
        
        # Find bills for this apartment
        apartment_bills = [bill for bill in manager.bills if bill.apartment == apartment.key]
        if apartment_bills:
            print_subsection_header("Bills")
            for bill in apartment_bills:
                month_year = f"{bill.settlement_month}/{bill.settlement_year}" if bill.settlement_month and bill.settlement_year else "N/A"
                print(f"      • {bill.type:<15} {format_currency(bill.amount_pln):>15}  Due: {bill.date_due}  Period: {month_year}")


def display_tenants(manager):
    """Display all tenants with their details and transfers"""
    print_section_header("TENANTS")
    
    for tenant in manager.tenants.values():
        print(f"\n👤 {tenant.name}")
        print(f"   Apartment: {tenant.apartment}")
        print(f"   Room: {tenant.room}")
        print(f"   Rent: {format_currency(tenant.rent_pln)}/month")
        print(f"   Deposit: {format_currency(tenant.deposit_pln)}")
        print(f"   Agreement: {tenant.date_agreement_from} to {tenant.date_agreement_to}")
        
        # Find transfers for this tenant
        tenant_transfers = [transfer for transfer in manager.transfers if transfer.tenant == tenant.name]
        if tenant_transfers:
            print_subsection_header("Transfers")
            for transfer in tenant_transfers:
                month_year = f"{transfer.settlement_month}/{transfer.settlement_year}" if transfer.settlement_month and transfer.settlement_year else "N/A"
                print(f"      • {format_currency(transfer.amount_pln):>15}  Date: {transfer.date}  Period: {month_year}")

def display_info_about_settlement(manager: Manager, apartment_key: str, year: int, month: int):
    apart_settlement = manager.get_settlement(apartment_key, year, month)
    if apart_settlement is None:

        return f"\nNie znaleziono mieszkania o kluczu '{apartment_key}' lub danych dla {month}/{year}."
    
    tenant_settlements = manager.create_tenants_settlements(apart_settlement)

    print_section_header(f"RAPORT: {apartment_key.upper()}")
    print(f"Okres: {month:02d}/{year}")
    print(f"Suma kosztów: {format_currency(apart_settlement.total_due_pln)}")
    print(f"Liczba osób: {len(tenant_settlements)}")
    print("-" *70)

    if tenant_settlements:
        print(f"{'LOKATOR':<25} | {'DO ZAPŁATY':>15}")
        print("-"*70)
        for t in tenant_settlements:
            print(f"{t.tenant:<25} | {format_currency(t.total_due_pln):>15}")
    else:
        print("Nie ma przypisanych lokatorów do tego mieszkania.")
    
    print("~" * 70)


if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    if len(sys.argv) == 4:
            try:
                apt_key = sys.argv[1]
                year = int(sys.argv[2])
                month = int(sys.argv[3])
                display_info_about_settlement(manager, apt_key, year, month)

            except ValueError:
                print("\nBłąd: Rok i miesiąc muszą być liczbami całkowitymi.")
    else:
        print("\nZła liczba argumentów. Przykład: python main.py apart-polanka 2024 1")
    