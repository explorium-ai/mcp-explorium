import EmptyState from "./EmptyState.svg";

export default function ChatEmptyState() {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center gap-4">
      <img src={EmptyState} alt="Empty State" className="w-16 aspect-square" />
      <p className="text-sm text-muted-foreground">
        Send a message to get started
      </p>
    </div>
  );
}
