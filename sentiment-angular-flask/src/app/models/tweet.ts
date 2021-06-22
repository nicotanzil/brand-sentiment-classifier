import {TwitterUser} from "./twitter-user";
import {Entity} from "./entity";

export class Tweet {
  id: number | undefined;
  text: string | undefined;
  user: TwitterUser = new TwitterUser();
  entities: Entity = new Entity();
  sentiment: string | undefined;
  created_at: Date | undefined;
  retweet_count!: number;
  reply_count!: number;
  favorite_count!: number;
}
