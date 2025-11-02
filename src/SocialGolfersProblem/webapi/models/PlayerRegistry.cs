namespace webapi.models;

public static class PlayerRegistry
{
        private const int _MAX_PLAYERS = 99;
        private static readonly Dictionary<int, string> _ID_TO_NAME = new Dictionary<int, string>();
        private static readonly Random _RNG = new Random();

        static PlayerRegistry()
        {
                InitializeRandomNames();
        }

        private static void InitializeRandomNames()
        {
                // Make a copy and shuffle it
                List<string> shuffled = new List<string>(_DEFAULT_NAMES);
                Shuffle(shuffled);

                // Fill the dictionary up to _MAX_PLAYERS
                for (int i = 0; i < _MAX_PLAYERS; i++)
                {
                        _ID_TO_NAME[i] = shuffled[i];
                }
        }

        private static void Shuffle(List<string> list)
        {
                for (int i = list.Count - 1; i > 0; i--)
                {
                        int j = _RNG.Next(i + 1);
                        (list[i], list[j]) = (list[j], list[i]);
                }
        }

        public static string GetNameById(int id)
        {
                if (_ID_TO_NAME.TryGetValue(id, out string? name))
                {
                        return name;
                }

                return $"Player_{id}";
        }


        // Because the frontend allows up to 99 players, here is a list of
        // 99 names. Obviously AI generated
        private static readonly List<string> _DEFAULT_NAMES = new List<string>
        {
                // RMA
                "Belling", "Vini", "Rodrygo", "Kroos", "Modric", "Bale", "Ramos", "Benzema",
                "Pepe", "Kaka", "Zidane", "Hierro", "Figo", "Gento", "Puskas", "Mijat", "Amavisca",
                "Sanchis", "Raul", "Butra", "Casemi", "Mendy", "Alaba", "Ceball", "Vazque",
                "Courto", "Arda",

                // Barca
                "Gavi", "Pedri", "Lewy", "De Jong", "Raphin", "Araujo", "Fati", "Busque",
                "Xavi", "Pique", "Puyol", "Alves", "Eto'o", "Deco", "Rivaldo", "Stoich",
                "Koeman", "Neeske", "Kluive", "Guardi", "Abreu", "Suarez", "Neymar",

                // PSG
                "Mbappe", "Marqui", "Hakimi", "Silva", "Verrat", "Icardi", "Cavani", "Paulet",
                "Weah", "Susaeta", "Digne", "Okocha", "Heinze", "Rabiot", "Lavezzi", "Vitinha",
                "Barco", "Mendes", "Sarabia",

                // Sparta
                "Kuchta", "Birman", "Precia", "Harasi", "Laci", "Rynes", "Kairin", "Sorens",
                "Hlozek", "Rosick", "Nedved", "Kolar", "Sionko", "Gresko", "Strake",

                // Legends
                "Pele", "Ronaldo", "Messi", "Muller", "Garrin", "Platini", "Baggio", "Beckham",
                "Giggs", "Rooney", "Terry", "Lampard", "Gerrard", "Shearer", "Kahn", "Buffon",
                "Zanetti", "Maldini", "Baresi", "Totti", "Sheva", "Forlan", "Aguer", "Salah",
                "Kane", "Haaland", "Son"
        };
}
