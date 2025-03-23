import { create } from "zustand";

interface ExploriumStore {
  apiKey: string | null;
  setApiKey: (apiKey: string) => void;
}

const useExploriumStore = create<ExploriumStore>((set) => ({
  apiKey: null,
  setApiKey: (apiKey: string) => set({ apiKey }),
}));

export default useExploriumStore;
