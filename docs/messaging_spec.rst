=========================
 Messaging Specification
=========================

--------------
 Introduction
--------------

SFM is architected as a number of components that exchange messages via a messaging
queue. To implement functionality, these components send and receive messages and perform
certain actions. The purpose of this document is to describe this interaction between the
components (called a "flow") and to specify the messages that they will exchange.

Note that as additional functionality is added to SFM, additional flows and messages
will be added to this document.

---------
 General
---------

* Messages may include extra information beyond what is specified below.
  Message consumers should ignore any extra information.
* RabbitMQ will be used for the messaging queue. See the Messaging docs for additional
  information. It is assumed in the flows below that components receive messages by
  connecting to appropriately defined queues and publish messages by submitting them
  to the appropriate exchange.

---------------------------------
 Harvesting social media content
---------------------------------

Harvesting is the process of retrieving social media content from the APIs
of social media services and writing to WARC files. It also includes extracting
urls for other web resources from the social media so that they can be
harvested by a web harvester. (For example, the link for an image may be extracted
from a tweet.)

Background information
======================
* A requester is an application that requests that a harvest be performed. A
  requester may also want to monitor the status of a harvest. In the current
  architecture, the SFM UI serves the role of requester.
* A stream harvest is a harvest that is intended to continue indefinitely until
  terminated. A harvest of a `Twitter public stream <https://dev.twitter.com/streaming/public>`_
  is an example of a stream harvest. A stream harvest is different from a non-stream
  harvest in that a requester must both start and optionally stop a stream harvest.
  Following the naming conventions from Twitter, a harvest of a REST, non-streaming API
  will be referred to as a REST harvest.
* Depending on the implementation, a harvester may produce a single warc or multiple warcs. It
  is likely that in general stream harvests will result in multiple warcs, but REST harvest will
  result in a single warc.

Flow
====

The following is the flow for a harvester performing a REST harvest and
creating a single warc:

1. Requester publishes a harvest start message.
2. Upon receiving the harvest message, a harvester:

   1. Makes the appropriate api calls.
   2. Extracts urls for web resources from the results.
   3. Writes the api calls to a warc.
3. Upon completing the api harvest, the harvester:

   1. Publishes a web harvest message containing the extracted urls.
   2. Publishes a warc created message.
   3. Publishes a harvest status message with the status of `completed success` or `completed failure`.


The following is the message flow for a harvester performing a stream harvest and
creating multiple warcs:

1. Requester publishes a harvest start message.
2. Upon receiving the harvest message, a harvester:

   1. Opens the api stream.
   2. Extracts urls for web resources from the results.
   3. Writes the stream results to a warc.
3. When rotating to a new warc, the harvester publishes a warc created message.
4. At intervals during the harvest, the harvester:

   1. Publishes a web harvest message containing extracted urls.
   2. Publishes a harvest status message with the status of `running`.
5. When ready to stop, the requester publishes a harvest stop message.
6. Upon receiving the harvest stop message, the harvester:

   1. Closes the api stream.
   2. Publishes a final web harvest message containing extracted urls.
   3. Publishes a final warc created message.
   4. Publishes a final harvest status message with the status of `completed success` or `completed failure`.

* Any harvester may send harvest status messages with the status of `running` before the final
  harvest status message. A harvester performing a stream harvest must send harvest status messages
  at regular intervals.
* A requester should not send harvest stop messages for a REST harvest. A harvester
  performing a REST harvest may ignore harvest stop messages.

Messages
========

Harvest start message
---------------------

Harvest start messages specify for a harvester the details of a harvest. Example::

    {
        "id": "sfmui:45",
        "type": "flickr_user",
        "seeds": [
            {
                "token": "justin.littman",
                "uid": "131866249@N02"
            },
            {
                "token": "library_of_congress"
            }
        ],
        "options": {
            "sizes": ["Thumbnail", "Large", "Original"]
        },
        "credentials": {
            "key": "abddfe6fb8bba36e8ef0278ec65dbbc8",
            "secret": "1642649c54cc3ebe"
        },
        "collection": {
            "id": "test_collection",
            "path": "/tmp/test_collection"
        }
    }

Another example::

    {
        "id": "test:1",
        "type": "twitter_search",
        "seeds": [
            {
                "token": "gwu"
            },
            {
                "token": "gelman"
            }
        ],
        "credentials": {
            "consumer_key": "EHde7ksBGgflbP5nUalEfhaeo",
            "consumer_secret": "ZtUpemtBkf2maqFiy52D5dihFPAiLebuMOmqN0jeQtXeAlen",
            "access_token": "481186914-c2yZjgbk13np0Z5MWEFQKSQNFBXd8T9r4k90YkJl",
            "access_token_secret": "jK9QOmn5Vbbmfg2ANT6KgfmKRqV8ThXVQ1G6qQg8BCejvp"
        },
        "collection": {
            "id": "test_collection",
            "path": "/tmp/test_collection"
        }
    }

* The routing key will be `harvest.start.<social media platform>.<type>`. For example,
  `harvest.start.flickr.flickr_photo`.
* `id`: A globally unique identifier for the harvest, assigned by the requester.
* `type`: Identifies the type of harvest, including the social media platform. The
  harvester can use this to map to the appropriate api calls.
* `seeds`: A list of seeds to harvest. Each seed is represented by a map containing `token` and (optionally) `uid`.
* `options`: A name/value map containing additional options for the harvest.  The contents of the map
  are specific to the type of harvest. (That is, the seeds for a flickr photo are going to be
  different than the seeds for a twitter user timeline.)
* `credentials`: All credentials that are necessary to access the social media platform.
  Credentials is a name/value map; the contents are specific to a social media platform.

Web resource harvest start message
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Harvesters will extract urls from the harvested social media content and
publish a web resource harvest start message. This message is similar to
other harvest start messages, with the differences noted below. Example::

    {
        "id": "flickr:45",
        "parent_id": "sfmui:45",
        "type": "web",
        "seeds": [
            {
                "token": "http://www.gwu.edu/"
            },
            {
                "token": "http://library.gwu.edu/"
            }
        ],
        "collection": {
            "id": "test_collection",
            "path": "/tmp/test_collection"
        }
    }

* The routing key will be `harvest.start.web`.
* `parent_id`: The id of the harvest from which the urls were extracted.

Harvest stop message
--------------------

Harvest stop messages tell a harvester perform a stream harvest to stop. Example::

    {
        "id": "sfmui:45"
    }

* The routing key will be `harvest.stop.<social media platform>.<type>`. For example,
  `harvest.stop.twitter.filter`.

Harvest status message
----------------------

Harvest status messages allow a harvester to provide information on the harvests
it performs. Example::

    {
        "id": "sfmui:45"
        "status": "completed success",
        "date_started": "2015-07-28T11:17:36.640044",
        "date_ended": "2015-07-28T11:17:42.539470",
        "infos": []
        "warnings": [],
        "errors": [],
        "summary": {
            "photo": 12,
            "user": 1
        },
        "token_updates": {
            "131866249@N02": "j.littman"
        },
        "uids": {
            "library_of_congress": "671366249@N03"
        },
        "warcs": {
            "count": 3
            "bytes": 345234242
        }
    }

* The routing key will be `harvest.status.<social media platform>.<type>`. For example,
  `harvest.status.flickr.flickr_photo`.
* `status`: Valid values are `completed success`, `completed failure`, or `running`.
* `infos`, `warnings`, and `errors`:  Lists of messages.  A message should be an object
  (i.e., dictionary) containing a `code` and `message` entry.  Codes should be consistent
  to allow message consumers to identify types of messages.
* `summary`:  A count of items that are harvested.  These should use human-understandable
  labels.  Summary is optional for in progress statuses, but required for final statuses.
* `token_updates`: A map of uids to tokens for which a token change was detected while harvesting.
  For example, for Twitter a token update would be provided whenever a user's screen name
  changes.
* `uids`: A map of tokens to uids for which a uid was identified while harvesting at not
  provided in the harvest start message.  For example, for Flickr a uid would be provided
  containing the NSID for a username.
* `warcs`.`count`: The total number of WARCs created during this harvest.
* `warcs`.`bytes`: The total number of bytes of the WARCs created during this harvest.

Warc created message
--------------------

Warc created message allow a harvester to provide information on the warcs that are
created during a harvest. Example::

    {
        "warc": {
            "path": "/var/folders/_d/3zzlntjs45nbq1f4dnv48c499mgzyf/T/tmpKwq9NL/test_collection/2015/07/28/11/test_collection-flickr-2015-07-28T11:17:36Z.warc.gz",
            "sha1": "7512e1c227c29332172118f0b79b2ca75cbe8979",
            "bytes": 26146,
            "id": "test_collection-flickr-2015-07-28T11:17:36Z",
            "date_created": "2015-07-28T11:17:36.640178"
        },
        "collection": {
            "path": "/var/folders/_d/3zzlntjs45nbq1f4dnv48c499mgzyf/T/tmpKwq9NL/test_collection",
            "id": "test_collection"
        }
    }

* The routing key will be `warc_created`.
* Each warc created message will be for a single warc.