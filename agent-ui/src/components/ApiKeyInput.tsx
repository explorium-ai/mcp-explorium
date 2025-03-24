import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import useExploriumStore from "@/store";
import { ExternalLink } from "lucide-react";

export default function ApiKeyInput() {
  const setApiKey = useExploriumStore((state) => state.setApiKey);

  return (
    <div className="m-auto">
      <h1 className="text-2xl font-bold">Explorium Research Agent Demo</h1>
      <p className="text-sm text-muted-foreground">
        Start by entering your API key below.
      </p>
      <form
        className="mt-4"
        onSubmit={(e) => {
          e.preventDefault();
          const form = e.target as HTMLFormElement;
          const apiKey = new FormData(form).get("apiKey") as string;
          setApiKey(apiKey);
        }}
      >
        <Input
          name="apiKey"
          placeholder="Enter your API key"
          className="font-mono bg-white"
        />
        <div className="flex mt-2 gap-2">
          <Button type="submit" variant="cta">
            Start
          </Button>
          <Button
            className="bg-black text-white cursor-pointer hover:bg-gray-900"
            asChild
          >
            <a
              href="https://developers.explorium.ai/reference/getting_your_api_key"
              target="_blank"
            >
              Get API Access
              <ExternalLink className="w-4 h-4" />
            </a>
          </Button>
        </div>
      </form>
    </div>
  );
}
