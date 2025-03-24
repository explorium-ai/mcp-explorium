import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUp } from "lucide-react";

interface ChatInputProps {
  onSubmit: (message: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSubmit, disabled }: ChatInputProps) {
  return (
    <form
      className="relative"
      onSubmit={(e) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const message = new FormData(form).get("message") as string;
        onSubmit?.(message);
        form.reset();
      }}
    >
      <Textarea
        className="resize-none h-24 pt-2 px-3 bg-white"
        disabled={disabled}
        name="message"
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            const form = e.currentTarget.form;
            if (form) {
              form.requestSubmit();
            }
          }
        }}
      />
      <Button
        onClick={() => {}}
        disabled={disabled}
        className="rounded-lg absolute right-2 bottom-2 w-10 h-10"
        type="submit"
      >
        <ArrowUp />
      </Button>
    </form>
  );
}
