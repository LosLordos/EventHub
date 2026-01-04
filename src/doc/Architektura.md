# Architektura – D1 (Repository Pattern)

## Vrstvy
- Domain: datové modely (Event, Customer, Venue, TicketOrder, Payment, EventParticipant)
- Repositories: přístup do DB (CRUD + dotazy), žádná business pravidla
- Services: business logika
  - TicketingService: transakce nákupu + hlídání kapacity + platba + účastník
  - ReportingService: report návštěvnosti a tržeb (+ agregace)
  - ImportingService: import customers a events + validace + protokol chyb
- API/UI: volají služby, mapují výjimky na srozumitelné chyby

## Repository metody (přehled)
- VenueRepository: list/get/create/update/delete
- CustomerRepository: list/get/create/update/delete, find_by_email
- EventRepository: list/get/create/update/delete, get_for_update(UPDLOCK)
- TicketOrderRepository: create, get, list_by_customer, set_status
- PaymentRepository: create, list_by_order
- EventParticipantRepository: add(event_id, customer_id) idempotentně
