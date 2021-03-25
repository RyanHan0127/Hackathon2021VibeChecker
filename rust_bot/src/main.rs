// Implements config.rs as a module
pub mod config;
use config::Config;

// Serenity is the Discord bot API for Rust!
use serenity::{
    async_trait,
    model::{channel::Message, gateway::Ready},
    prelude::*,
    framework::StandardFramework,
};

struct Handler; // more commonly known as "tard wrangler"

// The async_trait attribute from serenity allows us to do event handling
// asynchronously
#[async_trait]
impl EventHandler for Handler {
    // Set a handler for the `message` event - so that whenever a new message
    // is received - the closure (or function) passed will be called.
    //
    // Event handlers are dispatched through a threadpool, and so multiple
    // events can be dispatched simultaneously.
    //
    // Within this function we need to call the VADER thing and use
    // a match statement or other formula to determine output
    async fn message(&self, ctx: Context, msg: Message) {
        if msg.content == "!ping" {
            // Sending a message can fail, due to a network error, an
            // authentication error, or lack of permissions to post in the
            // channel, so log to stdout when some error happens, with a
            // description of it.
            if let Err(why) = msg.channel_id.say(&ctx.http, "Pong!").await {
                println!("Error sending message: {:?}", why);
            }
        }
    }

    // Set a handler to be called on the `ready` event. This is called when a
    // shard is booted, and a READY payload is sent by Discord. This payload
    // contains data like the current user's guild Ids, current user data,
    // private channels, and more.
    //
    // In this case, just print what the current user's username is.
    async fn ready(&self, _: Context, ready: Ready) {
        println!("{} is connected!", ready.user.name);
    }
}

// Tokio is a crate used for asynchronous io, perfect for event handling
// in cases like a discord bot!
//
// In order to make the main function asynchronous we have to apply the
// "main" attribute from tokio
#[tokio::main]
async fn main() {
    // Configure the config file so that the token and prefix can be accessed.
    let _ = Config::new().save();
    let config = Config::load().unwrap();

    // Implement the standard framework for the client
    let framework = StandardFramework::new()
        .configure(|c| c
            .with_whitespace(true)
            .prefix(config.prefix()));

    // Create a new instance of the Client, logging in as a bot. This will
    // automatically prepend your bot token with "Bot ", which is a requirement
    // by Discord for bot users.
    let mut client = Client::builder(config.token())
        .event_handler(Handler)
        .framework(framework)
        .await
        .expect("Err creating client");

    // Finally, start a single shard, and start listening to events.
    //
    // Shards will automatically attempt to reconnect, and will perform
    // exponential backoff until it reconnects.
    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}
