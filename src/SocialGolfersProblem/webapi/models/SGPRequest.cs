namespace webapi.models;

public struct SGPRequest
{
        public int N;
        public int R;
        public int G;
        public int S;
        public int T;

        public SGPRequest(int N, int R, int G, int S, int T)
        {
                this.N = N;
                this.R = R;
                this.G = G;
                this.S = S;
                this.T = T;
        }
}
