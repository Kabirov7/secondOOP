import netfLix
import kino_afisha
import seriaLs

def main():
    cinema = kino_afisha.kino_afisha()
    cinema.main()

    netflix_serials = netfLix.netflix()
    netflix_serials.main()

    serial = seriaLs.serials()
    serial.main()

main()