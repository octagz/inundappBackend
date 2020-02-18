<?php

namespace AppBundle\Controller;

use Sensio\Bundle\FrameworkExtraBundle\Configuration\Route;
use Sensio\Bundle\FrameworkExtraBundle\Configuration\Method;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use AppBundle\Entity\Evento;
use AppBundle\Form\TipoEvento;
use AppBundle\Entity\Imagen;
use AppBundle\Controller\NotificationControllerTesting;

class ApiControllerTesting extends Controller {

    public function __construct() {

        $this->notifications = new NotificationControllerTesting();
    }

    /**
     * @Route("/api/testing/eventos")
     * @Method("GET")
     */
    public function GetEventosAction(Request $request) {

        //Recupero el repositorio para los eventos
        $repositorio = $this->getDoctrine()->getRepository('AppBundle:Evento');

        $eventos = $repositorio->findAll();
        $eventosSerializados = array();
        foreach($eventos as $e){
            array_push($eventosSerializados,$this->serializarEvento($e));
        }
        $response = new Response(json_encode($eventosSerializados), 200);
	      $response->headers->set('Access-Control-Allow-Origin', $request->headers->get('origin'));
        return $response;
    }
    
     /**
     * @Route("/api/testing/eventos/{FI}/{FF}")
     * @Method("GET")
     */
    public function GetEventosPorFechaAction($FI, $FF,Request $request) {
         
       //SANITIZE ENTRIES AND VALIDATE (ff >= fi)
       //Error con codigo 204 no content
        
          
            $FI = filter_var($FI, FILTER_SANITIZE_NUMBER_INT);
            $FF = filter_var($FF, FILTER_SANITIZE_NUMBER_INT);
            $FI = str_replace('+','',$FI);
            $FI = str_replace('-','',$FI);
            $FF = str_replace('+','',$FF);
            $FF = str_replace('-','',$FF);
                    
       if (($FI != "")&&($FF != "")&&($FF >= $FI)) {
        
            //Recupero el repositorio para los eventos
            $em = $this->getDoctrine()->getEntityManager();

            //Formateo los timestamp a datetime. El mismo date resta el offset de 10800 s 
            //Date toma por default al timestamp en GMT
            $FI = date('Y-m-d H:i:s',$FI);
            $FF = date('Y-m-d H:i:s',$FF);
            
            //Recupero los eventos en el intervalo de tiempo (FI,FF)
            $query = $em->createQuery('
                  SELECT e FROM 
                          AppBundle:Evento e
                       WHERE
                          e.fecha >= :FI AND e.fecha <= :FF
                       ORDER BY 
                          e.fecha ASC
                  ')->setParameter('FI', $FI)
                    ->setParameter('FF', $FF);

            $eventos = $query->getResult();

            //Serializo los eventos
            $eventosSerializados = array();
              foreach($eventos as $e){
                  array_push($eventosSerializados,$this->serializarEvento($e));
              }
            $response = new Response(json_encode($eventosSerializados), 200);
       }else {
               $response = new Response("[]",400);
            }   
      $response->headers->set('Access-Control-Allow-Origin', $request->headers->get('origin'));
      return $response;
      }
    
      /**
     * @Route("/api/testing/eventos/{id}")
     * @Method("GET")
     */
    public function GetEventoAction($id,Request $request) {
      
       //Recupero el repositorio para los eventos
        $repositorio = $this->getDoctrine()->getRepository('AppBundle:Evento');
        
       $criterio = array('id' => $id);
        
       //findOneBy valida en base al criterio(id) todos los casos.
       $evento = $repositorio->findOneBy($criterio);
       
       if (!$evento) {
          
          return new Response("[]",404);   
        }
	     $response = new Response(json_encode($this->serializarEvento($evento)), 200);
       $response->headers->set('Access-Control-Allow-Origin', $request->headers->get('origin'));

      return $response;
        
    }

    /**
      * @Route("/api/testing/eventos/{id}")
      * @Method("PUT")
      */
    public function subirImagen(Request $request, $id) {

       //Recupero el repositorio para los eventos
        $repositorio = $this->getDoctrine()->getRepository('AppBundle:Evento');
        
       $criterio = array('id' => $id);
        
       //findOneBy valida en base al criterio(id) todos los casos.
       $evento = $repositorio->findOneBy($criterio);

       $imagen = new Imagen();

       //Estamos seguros que el evento existe y es levantando de la bd
       $data = $request->getContent();

       if ($imagen->upload($data) === FALSE) {
          $response = new Response('Ocurrio un error al subir la imagen.',400);      
       }
       else { //Successful upload!

          $evento->addIdImagen($imagen);
          //Recupero el entity manager
          $em = $this->getDoctrine()->getManager();

          //Guardo los cambios en la bd
//           $em->persist($imagen);
//           $em->persist($evento);
//           $em->flush();

          $response = new Response('Upload completado',201);    
       }

    	$response->headers->set('Access-Control-Allow-Origin', $request->headers->get('origin'));

    	return $response;

    }

    
    /**
     * @Route("/api/testing/eventos")
     * @Method("POST")
     */
    public function CrearEvento(Request $request) {
        
        $data = json_decode($request->getContent(), true);
        $evento = new Evento();
        $validator = $this->get('validator');
        $form = $this->createForm(new TipoEvento(), $evento);
        $form->submit($data);
        
        //Valido los datos del evento
        $errors = $validator->validate($evento);
        if (!count($errors)) {

         $em = $this->getDoctrine()->getManager();

            //$em->persist($evento);
            //$em->flush();

            //Send push notification
            $this->notifications->sendNotification($this->serializarEvento($evento));

            $response = new Response(json_encode(
              array(
                'upload_uri' => urlencode($evento->getId()))
              )
            ,201);
         } else {
            $response = new Response($errors, 400);
         }

	$response->headers->set('Access-Control-Allow-Origin', $request->headers->get('origin'));

	return $response;
    }
    
     private function serializarEvento(Evento $evento)
    {
        return array(
            'latitud' => $evento->getLatitud(),
            'longitud' => $evento->getLongitud(),
            'fecha' => $evento->getFecha(),
            'id' => $evento->getId(),
            'afectaciones' =>$this->serializarAfectacion($evento->getNombreAfectacion()),
            'fenomeno'=>$evento->getFenomeno(),
            'imagenes'=>$this->serializarImagen($evento->getIdImagen())
            );
    }
    
    private function serializarAfectacion($afectaciones) {
        
        $afectacionesSerializadas = array();
        foreach($afectaciones as $a){
            array_push($afectacionesSerializadas,$a->getNombre());
         }
         
        return $afectacionesSerializadas;
    }

    private function serializarImagen($imagenes) {
        
        $imagenesSerializadas = array();
        if (!is_null($imagenes))
            foreach($imagenes as $i){
                array_push($imagenesSerializadas,urlencode($this->URLSitio().$i->getWebPath()));
            }
         
        return $imagenesSerializadas;
    }

    function URLSitio()
    {
        $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' || $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";
        $domainName = $_SERVER['HTTP_HOST'].'/';
        return $protocol.$domainName;
    }
}
