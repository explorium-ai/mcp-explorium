import useExploriumStore from "@/store";
import ApiKeyInputScreen from "@/screens/ApiKeyInputScreen";
import ChatScreen from "@/screens/ChatScreen";

export default function App() {
  const apiKey = useExploriumStore((state) => state.apiKey);

  return (
    <div className="h-screen bg-explorium-bg">
      {apiKey ? <ChatScreen /> : <ApiKeyInputScreen />}
    </div>
  );
}
