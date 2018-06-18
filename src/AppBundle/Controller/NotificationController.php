<?php

namespace AppBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class NotificationController extends Controller {

    /**
     * @var string
     */
    private $CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS';

    /**
     * google service scope (firebase.messaging)
     */
    private $scope = 'https://www.googleapis.com/auth/firebase.messaging';

    /**
     * firebase project ID
     */
    private $projectId;

    /**
     * instance of GuzzleHttp\Client that authenticates with the Google API.
     */
    private $httpClient;

    /**
     * generic firebase endpoint url
     */
    private $endpoint = 'https://fcm.googleapis.com/v1/projects';
    
    /**
     * firebase endpoint method
     */
    private $endpoint_method = 'messages:send';


    public function __construct()
    {
        //Load service account credentials
        $this->setCredentials();
        //Get GuzzleHttp\Client
        $this->setClient();;
    }

    private function setCredentials() {

        $credentialsPath =  realpath("../src/AppBundle/Resources/config/pushnotifications"). 
                            '/inund4pp2018push-firebase-adminsdk-pv6yb-8e3bfba679.json';
        putenv( $this->CREDENTIALS . '=' . $credentialsPath );
        //Get Firebase project id
        $content = file_get_contents($credentialsPath);
        $json_content = json_decode($content, true);
        $this->projectId = $json_content['project_id']; //according to service_account.json
    }

    private function setClient() {

        $this->client = new \Google_Client();
        // Authentication with the GOOGLE_APPLICATION_CREDENTIALS environment variable
        $this->client->useApplicationDefaultCredentials();
        // Add the scope as a string (multiple scopes can be provided as an array)
        $this->client->addScope($this->scope);
        // Get authenticated GuzzleHttp/Client
        $this->httpClient = $this->client->authorize();
    }

    private function getEndpointURL() {

        return $this->endpoint
                . '/'
                . $this->projectId
                . '/'
                . $this->endpoint_method;
    }

    //Por ahora solo config stuff para Android
    private function generateBaseMessage() {

        //!('TopicA' in topics)
        //any app instances that are not subscribed to TopicA, including app instances that are not subscribed to any topic, receive the message.
        //'TopicA' in topics && ('TopicB' in topics || 'TopicC' in topics)
        //FCM first evaluates any conditions in parentheses, and then evaluates the expression from left to right.
        //You can include up to five topics in your conditional expression, and parentheses are supported. Supported operators: &&, ||, !.


        $topic_events = "inundapp_events";
        $topic_sender = "inundapp_event_sender";
        $condition = "'" . $topic_events . "' in topics";

        $message  = [ 
                "condition"                     => $condition,
                "android"                       => [
                    "ttl"                       => "21600s", //ttl de eventos relevantes es de 6 horas
                    "restricted_package_name"   => "com.cs.uns.edu.ar.inundapp",
                    "notification"              => [
                        "icon"                  => "push_icon",
                        "color"                 => "##82b3c9",
                        "sound"                 => "default", //notification sound
                        "click_action"          => "FCM_PLUGIN_ACTIVITY",  //Must be present for Android FCM plugin
                    ]
                ]
        ];

       return $message;
    }

    private function prepararTitle($fenomeno) {
        
        return 'Detectamos ' . $fenomeno . ' en la zona!';
    }

    private function prepararBody($afectaciones) {

        $length = count($afectaciones);
        $body = 'Daños registrados en ' . array_shift($afectaciones);
        if ($length >= 2) {
            $last = array_pop($afectaciones);
            foreach($afectaciones as $afectacion) {
                $body = $body . ', ' . $afectacion;
             };
            $body = $body . ' y ' . $last;

         };
        $body = $body . '.';

        return $body;
    }

    private function setNotification($evento) {

        $baseMessage = $this->generateBaseMessage();
        $title = $this->prepararTitle($evento['fenomeno']);
        $body = $this->prepararBody($evento['afectaciones']);

        $notification =  [
            "data"                      => [
                "evento_id"                 => (string)$evento['id'],
                "evento_fenomeno"           => $evento['fenomeno']
            ],
            "notification"              => [
                "body"                  => $body,
                "title"                 => $title
            ]                    
        ];

        $result = array_merge($baseMessage, $notification);

        $message['message'] = $result;
        
        return $message;
    }

    public function sendNotification($evento) {

       $url = $this->getEndpointURL();
       $message = $this->setNotification($evento);
       // Send the Push Notification - use $response to inspect success or errors
       $response = $this->httpClient->post( $url, ['json' => $message]);
    }

}