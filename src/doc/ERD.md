# ERD – EventHub

## Entity
- Venue (místo) 1:N Event (akce)
- Customer (zákazník) 1:N TicketOrder (objednávka)
- Event (akce) 1:N TicketOrder (objednávka)
- TicketOrder 1:N Payment (platba)
- Event M:N Customer přes EventParticipant (účastníci)

## Poznámky
- Kapacita se hlídá transakčně: při koupi se zamkne Event řádek, ověří se (Capacity - SoldCount) a až pak se navýší SoldCount.
- EventParticipant se zapisuje po zaplacení (nebo přímo v rámci nákupu, pokud nákup = okamžitě Paid).
