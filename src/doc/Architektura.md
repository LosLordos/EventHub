# Architektura (D1 – Repository)

## Vrstvy
- Domain (src/app/domain): datové modely + typy (bez DB)
- Repositories (src/app/repositories): čisté CRUD + dotazy nad DB (bez business pravidel)
- Services (src/app/services): business logika:
  - ticketing: transakce nákupu + kapacita + platba + zápis účastníka
  - reporting: návštěvnost + tržby (agregace z 3+ tabulek / view)
  - importing: import CSV (customers), CSV (events)
- API (src/app/api): REST endpointy
- UI (src/app/ui + templates): jednoduché HTML stránky nad services

## Typické repository metody
- VenueRepository: list/get/create/update/delete
- EventRepository:
  - list/get/create/update/delete
  - lock_for_update(event_id) / get_for_update s UPDLOCK
  - increment_sold(event_id, qty) s kontrolou kapacity
- CustomerRepository: list/get/create/update/delete + find_by_email
- TicketOrderRepository: create, get, list_by_customer, set_status
- PaymentRepository: create, list_by_order
- EventParticipantRepository: add_participant(event_id, customer_id) (idempotentní)


