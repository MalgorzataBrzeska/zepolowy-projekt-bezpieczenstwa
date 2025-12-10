# Raport bezpieczeństwa środowiska - zadanie 2

**[ID-003] Audyt bezpieczeństwa systemu Kali Linux wykonany za pomocą Lynis**

Został przeprowadzony audyt bezpieczeństwa systemu Kali Linux za pomocą Lynis.
Celem testu jest wykrycie luk bądź błędów konfiguracyjnych, które wpływają na bezpieczeństwo systemu. 
Podczas testów zostały wykryte ostrzeżenia i rekomendacje poprawiające stan bezpieczeństwa.

## Wykryte zagorzenia
1. Brak aktywnych reguł zapory sieciowej,
2. Brak narzędzi wspierających kontrolę pakietów, aktualizacji oraz restart usług.
3. Brak mechanizmów obrony przed atakami brute-force (Fail2ban)
4. Ryzyko fizycznej modyfikacji ustawień rozruchu (GRUB bez hasła)

## Ostrzeżenia i sugestie wygenerowane przez Lynis

1. **NETW-2705 — Brak dwóch responsywnych serwerów DNS**

Brak skonfigurowanych poprawnie działających DNS. Skutkiem tego mogą być problemy sieciowe i brak redundancji.

**zalecenie:** Dodać co najmniej 2 DNS do pliku /etc/resolv.conf 

2. **FIRE-4512 — Załadowany moduł iptables, ale brak aktywnych reguł**

Firewall został wykryty, natomiast nie działa żadna reguła ochronna.

**zalecenie:**  Konfiguracja iptables/ufw/nftables.