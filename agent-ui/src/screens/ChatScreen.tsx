import ChatInput from "@/components/ChatInput";
import ChatMessages from "@/components/ChatMessages";
import useExploriumStore from "@/store";
import { Message } from "@langchain/langgraph-sdk";
import { useStream } from "@langchain/langgraph-sdk/react";
import { useCallback } from "react";

export default function ChatScreen() {
  const thread = useStream<{ messages: Message[] }>({
    apiUrl: "http://localhost:2024",
    assistantId: "research_agent",
    messagesKey: "messages",
  });
  const apiKey = useExploriumStore((state) => state.apiKey);

  const onSendMessage = useCallback(
    (message: string) => {
      thread.submit(
        { messages: [{ type: "human", content: message }] },
        {
          config: {
            configurable: {
              explorium_api_key: apiKey,
            },
          },
        }
      );
    },
    [thread, apiKey]
  );

  return (
    <div className="mx-auto h-full flex flex-col pb-4">
      <div className="flex-1 overflow-y-auto">
        <ChatMessages messages={thread.messages ?? []} />
      </div>
      <div className="w-[768px] mx-auto">
        <ChatInput onSubmit={onSendMessage} disabled={thread.isLoading} />
      </div>
    </div>
  );
}
