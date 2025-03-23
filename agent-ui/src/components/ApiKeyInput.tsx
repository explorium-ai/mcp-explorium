import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import useExploriumStore from "@/store";

export default function ApiKeyInput() {
  const setApiKey = useExploriumStore((state) => state.setApiKey);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        const form = e.target as HTMLFormElement;
        const apiKey = new FormData(form).get("apiKey") as string;
        setApiKey(apiKey);
      }}
    >
      <Input name="apiKey" placeholder="Enter your API key" />
      <Button type="submit">Save</Button>
    </form>
  );
}
