<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;
/**
 * Imagen
 */
class Imagen
{
      /**
     * @var string
     */
    private $nombre;

    /**
     * @var string
     */
    private $path;

    /**
     * @var integer
     */
    private $id;

    /**
     * @var \Doctrine\Common\Collections\Collection
     */
    private $idEvento;

    /**
     * @Assert\File(maxSize="6000000")
     * @Assert\Image(
     *     allowLandscape = false,
     *     allowPortrait = false
     * )
     */
    private $file;

    /**
     * Sets archivo.
     *
     * @param UploadedFile $file
     */
    public function setFile(UploadedFile $file = null)
    {
        $this->file = $file;
    }

        /**
     * Get archivo.
     *
     * @return UploadedFile
     */
    public function getFile()
    {
        return $this->file;
    }

      public function getAbsolutePath()
    {
        return null === $this->path
            ? null
            : $this->getUploadRootDir().'/'.$this->path;
    }

    public function getWebPath()
    {
      //Este web path es el que usamos en el template para linkear a la imagen
        return null === $this->path
            ? null
            : $this->getUploadDir().'/'.$this->path;
    }

    protected function getUploadRootDir()
    {
        //Este es el path absoluto donde se guardan las fotos
        
        return __DIR__.'/../../../web/'.$this->getUploadDir();
    }

    protected function getUploadDir()
    {
        // get rid of the __DIR__ so it doesn't screw up
        // when displaying uploaded doc/image in the view.
        return 'images/uploads/';
    }

     public function upload()
    {
    //Puede pasar que no se haya cargado ninguna imagen
    if (null !== $this->getFile()) {
   
    // use the original file name here but you should
    // sanitize it at least to avoid any security issues

    // compute a random name and try to guess the extension (more secure)
        $extension = $this->getFile()->guessExtension();
        if (!$extension) {
            //No se puede calcular la extension
            $extension = 'png'; //Seteo extension default
        }

    //Construyo el path para la imagen
     $path_recuperado = rand(1, 99999).'.'.$extension;
      
    $this->getFile()->move(
        $this->getUploadRootDir(), //directorio
         $path_recuperado //nombre de la imagen de la afectacion
        );

    //Seteo el path del filename donde guardo la imagen
    $this->path = $path_recuperado;

    //Una vez que movi el archivo, este atributo ya no interesa asique lo limpio
    $this->file = null;
      
    }
}
    

    /**
     * Constructor
     */
    public function __construct()
    {
        $this->idEvento = new \Doctrine\Common\Collections\ArrayCollection();
    }

    /**
     * Set nombre
     *
     * @param string $nombre
     * @return Imagen
     */
    public function setNombre($nombre)
    {
        $this->nombre = $nombre;

        return $this;
    }

    /**
     * Get nombre
     *
     * @return string 
     */
    public function getNombre()
    {
        return $this->nombre;
    }

    /**
     * Set path
     *
     * @param string $path
     * @return Imagen
     */
    public function setPath($path)
    {
        $this->path = $path;

        return $this;
    }

    /**
     * Get path
     *
     * @return string 
     */
    public function getPath()
    {
        return $this->path;
    }

    /**
     * Get id
     *
     * @return integer 
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Add idEvento
     *
     * @param \AppBundle\Entity\Evento $idEvento
     * @return Imagen
     */
    public function addIdEvento(\AppBundle\Entity\Evento $idEvento)
    {
        $this->idEvento[] = $idEvento;

        return $this;
    }

    /**
     * Remove idEvento
     *
     * @param \AppBundle\Entity\Evento $idEvento
     */
    public function removeIdEvento(\AppBundle\Entity\Evento $idEvento)
    {
        $this->idEvento->removeElement($idEvento);
    }

    /**
     * Get idEvento
     *
     * @return \Doctrine\Common\Collections\Collection 
     */
    public function getIdEvento()
    {
        return $this->idEvento;
    }

}
