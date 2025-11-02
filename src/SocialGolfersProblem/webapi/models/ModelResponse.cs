namespace webapi.models;

public class ModelResponse
{
        public List<Round> Rounds;
        public bool UNSAT = false;

        public ModelResponse(string modelPath, int roundCount)
        {
                Rounds = new List<Round>(roundCount);
                LoadModel(modelPath);
        }

        private void LoadModel(string modelPath)
        {
                try
                {
                        StreamReader sr = new StreamReader(modelPath);
                        while (!sr.EndOfStream)
                        {
                                var line = sr.ReadLine();
                                if (line != null)
                                {
                                        line = line.Trim();

                                        // Trivial case
                                        if (line == "UNSAT")
                                        {
                                                UNSAT = true;
                                                return;
                                        }

                                        var round = new Round();
                                        string[] groupStrings = line.Split(';', StringSplitOptions.RemoveEmptyEntries);

                                        foreach (string groupStr in groupStrings)
                                        {
                                                var group = new Group();
                                                string[] playersIDs = groupStr.Split(',', StringSplitOptions.RemoveEmptyEntries);

                                                foreach (string playerId in playersIDs)
                                                {
                                                        if (int.TryParse(playerId, out int id))
                                                        {
                                                                var name = PlayerRegistry.GetNameById(id);
                                                                group.Players.Add(name);
                                                        }
                                                }

                                                round.Groups.Add(group);
                                        }

                                        Rounds.Add(round);
                                }
                        }
                }
                catch (Exception e)
                {
                        // TODO Handle the exception
                }
        }
}
